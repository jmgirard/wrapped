"""S4: turn Quarto's one-cell figure tables into Word frames.

Usage: python3 -I frame.py s4.docx s4-framed.docx

For each figure table, the script removes the table and puts the same
w:framePr on the image paragraph and the caption paragraph, so Word merges
them into one frame. Two forms are tested:

- fig-right: one merged w:pPr per paragraph, in schema order.
- fig-left: the frame goes in an extra w:pPr in front of the existing ones.
  A filter that adds raw OpenXML puts it after Pandoc's own w:pPr instead,
  so this is not that filter's order.
"""

import re
import sys
import zipfile

EMU_PER_TWIP = 635
GAP_TWIPS = 240  # 1em at 12pt

FIGURES = {"fig-right": ("right", "merged"), "fig-left": ("left", "extra")}


def frame_pr(width_twips, side):
    return (
        f'<w:framePr w:w="{width_twips}" w:wrap="around" w:hSpace="{GAP_TWIPS}" '
        f'w:vAnchor="text" w:hAnchor="margin" w:xAlign="{side}"/>'
    )


def merged_ppr(ppr_block, frame):
    """Merge every w:pPr child into one w:pPr, with w:framePr after w:pStyle."""
    known = {"pStyle", "spacing", "jc"}
    found = set(re.findall(r"<w:(\w+)\b", ppr_block)) - {"pPr"}
    if found - known:
        sys.exit(f"unexpected w:pPr children: {sorted(found - known)}")
    style = re.search(r'<w:pStyle\b[^>]*/>', ppr_block)
    spacing = re.search(r'<w:spacing\b[^>]*/>', ppr_block)
    # The last w:jc wins, as Quarto's caption carries center then left.
    jcs = re.findall(r'<w:jc\b[^>]*/>', ppr_block)
    out = "<w:pPr>"
    if style:
        out += style.group(0)
    out += frame
    if spacing:
        out += spacing.group(0)
    if jcs:
        out += jcs[-1]
    out += "</w:pPr>"
    return out


def frame_paragraph(p, frame, form):
    m = re.match(r"(<w:p>)((?:\s*<w:pPr>.*?</w:pPr>)*)(.*)", p, re.S)
    head, pprs, rest = m.groups()
    if form == "merged":
        return head + merged_ppr(pprs, frame) + rest
    return head + "<w:pPr>" + frame + "</w:pPr>" + pprs + rest


def unwrap_figure(xml, fig_id, side, form):
    tbl_re = re.compile(
        r"<w:tbl>(?:(?!</w:tbl>).)*?w:name=\"" + fig_id + r"\".*?</w:tbl>", re.S
    )
    m = tbl_re.search(xml)
    if not m:
        sys.exit(f"figure table {fig_id} not found")
    tbl = m.group(0)
    cell_match = re.search(r"<w:tcPr\s*/>(.*)</w:tc>", tbl, re.S)
    if not cell_match:
        sys.exit(f"figure table {fig_id} has no empty w:tcPr cell")
    cell = cell_match.group(1)
    cx = int(re.search(r'<wp:extent cx="(\d+)"', cell).group(1))
    width_twips = cx // EMU_PER_TWIP
    frame = frame_pr(width_twips, side)
    paragraphs = re.findall(r"<w:p>.*?</w:p>", cell, re.S)
    new_cell = cell
    for p in paragraphs:
        new_cell = new_cell.replace(p, frame_paragraph(p, frame, form), 1)
    return xml[: m.start()] + new_cell + xml[m.end():]


def main(src, dst):
    with zipfile.ZipFile(src) as zin:
        xml = zin.read("word/document.xml").decode("utf-8")
        for fig_id, (side, form) in FIGURES.items():
            xml = unwrap_figure(xml, fig_id, side, form)
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = xml.encode("utf-8")
                zout.writestr(item, data)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
