"""Layout checks for the wrapped figures on the docs site's example pages.

Render the site first (`quarto render docs`), then run from the repository
root:

    python3 tests/docs_layout.py

It reads the PDF through LaTeX, the PDF through Typst, and a LibreOffice PDF
of the Word file of each page in CASES, and exits with status 1 if a figure
fails. For each wrapped figure, the page must have:

- a paragraph of at least two lines before the figure, each line but the
  last crossing the figure's horizontal span, and
- a paragraph after the figure with a line beside the figure and a later
  line below the figure's bottom that crosses its span.

A line crosses the span of a right-side figure when its right edge is right
of the figure's left edge, and of a left-side figure when its left edge is
left of the figure's right edge. The figure's bottom is the lower of its
image and its last caption line. All of it must be on one page.

`python3 tests/docs_layout.py --js` prints the call that runs the same
check in a browser with `straddle()` from tests/layout.js.
"""

import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs" / "_site"

# Per page, one entry per wrapped figure in page order. `above` and
# `straddle` name the first and last word of the paragraph before the figure
# and of the paragraph that runs beside and below it. Each word is searched
# for, as part of a text element, after the one before it, so a word that
# also occurs earlier is fine.
CASES = {
    "examples/image-figure": [
        {"side": "right", "above": ["comes", "markdown:"], "straddle": ["paragraphs", "Word."]},
    ],
}

TOL = 2  # px, in pdftohtml's 1.5 px per pt


def pdf_paths(page, tmp):
    """The three PDFs of a page: LaTeX, Typst, and Word through LibreOffice."""
    base = SITE / page
    docx = base.with_suffix(".docx")
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(docx)],
        check=True, capture_output=True,
    )
    return {
        "latex": base.with_suffix(".pdf"),
        "typst": base.parent / f"{base.name}-typst.pdf",
        "word": Path(tmp) / f"{base.name}.pdf",
    }


def read_pdf(pdf, tmp):
    """Text elements in stream order and image boxes, each with its page."""
    out = Path(tmp) / f"{pdf.stem}-{abs(hash(str(pdf)))}"
    subprocess.run(["pdftohtml", "-xml", "-q", str(pdf), str(out)], check=True, capture_output=True)
    root = ET.parse(f"{out}.xml").getroot()
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
            elif el.tag == "text":
                box["text"] = "".join(el.itertext())
                texts.append(box)
    images.sort(key=lambda b: (b["page"], b["top"]))
    return texts, images


def norm(s):
    """Text with the letters that LibreOffice's PDF loses taken out.

    In a LibreOffice PDF of the docx, pdftohtml drops "e" and "g" and
    doubles some letters ("Fi ur ", "bottrom"), so a marker is matched with
    those letters, spaces, and soft hyphens removed and doubled letters
    made single.
    """
    s = re.sub(r"[eEgG\s\u00ad]", "", s).lower()
    return re.sub(r"(.)\1+", r"\1", s)


def find(texts, word, start):
    for i in range(start, len(texts)):
        if norm(word) in norm(texts[i]["text"]):
            return i
    raise LookupError(f"no word {word!r}")


def lines(elements):
    """Merge text elements into lines by page and top."""
    out = []
    for el in elements:
        for line in out:
            if line["page"] == el["page"] and abs(line["top"] - el["top"]) <= 3:
                line["left"] = min(line["left"], el["left"])
                line["right"] = max(line["right"], el["right"])
                line["bottom"] = max(line["bottom"], el["bottom"])
                break
        else:
            out.append({k: el[k] for k in ("page", "top", "bottom", "left", "right")})
    return sorted(out, key=lambda l: (l["page"], l["top"]))


def crosses(line, fig):
    if fig["side"] == "right":
        return line["right"] > fig["left"] + TOL
    return line["left"] < fig["right"] - TOL


def check(texts, image, case, pos):
    """Returns (problems, next search position) for one figure."""
    problems = []
    a0 = find(texts, case["above"][0], pos)
    a1 = find(texts, case["above"][1], a0)
    s0 = find(texts, case["straddle"][0], a1 + 1)
    s1 = find(texts, case["straddle"][1], s0)
    fig = dict(image, side=case["side"])
    # Caption lines sit inside the image's span, just below it.
    for t in texts:
        if (t["page"] == fig["page"] and t["left"] >= image["left"] - 30
                and t["right"] <= image["right"] + 30
                and 0 <= t["top"] - fig["bottom"] <= 40):
            fig["bottom"] = t["bottom"]
            fig["left"] = min(fig["left"], t["left"])
            fig["right"] = max(fig["right"], t["right"])
    # Typst and Word can put caption lines among the paragraph's text.
    def outside(t):
        return not (t["page"] == fig["page"] and t["left"] >= fig["left"] - TOL
                    and t["right"] <= fig["right"] + TOL
                    and t["top"] >= fig["top"] - TOL and t["bottom"] <= fig["bottom"] + TOL)
    above = lines([t for t in texts[a0:a1 + 1] if outside(t)])
    para = lines([t for t in texts[s0:s1 + 1] if outside(t)])
    pages = {l["page"] for l in above + para} | {fig["page"]}
    if len(pages) > 1:
        problems.append(f"spans pages {sorted(pages)}")
    if len(above) < 2:
        problems.append(f"paragraph above has {len(above)} line")
    elif not all(crosses(l, fig) for l in above[:-1]):
        problems.append("a line above does not cross the figure")
    beside = [l for l in para if l["bottom"] > fig["top"] and l["top"] < fig["bottom"] and not crosses(l, fig)]
    below = [l for l in para if l["top"] >= fig["bottom"] - TOL and crosses(l, fig)]
    if not beside:
        problems.append("no line of the paragraph beside the figure")
    elif not any(l["top"] > beside[0]["top"] for l in below):
        problems.append("no later line below the figure that crosses it")
    return problems, s1 + 1


def main():
    if "--js" in sys.argv:
        for page, cases in CASES.items():
            print(f"{page}.html: m.straddle({json.dumps(cases)})")
        return 0
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for page, cases in CASES.items():
            for fmt, pdf in pdf_paths(page, tmp).items():
                texts, images = read_pdf(pdf, tmp)
                pos = 0
                for n, case in enumerate(cases):
                    try:
                        image = images[n]
                        problems, pos = check(texts, image, case, pos)
                    except (LookupError, IndexError) as e:
                        problems = [str(e) or "no image"]
                    status = "ok" if not problems else "FAIL: " + "; ".join(problems)
                    failed += bool(problems)
                    print(f"{page} {fmt} figure {n + 1}: {status}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
