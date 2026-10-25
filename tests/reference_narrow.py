"""Write tests/reference-narrow.docx, the reference doc of docx-reference.qmd.

Run from the repository root:

    python3 tests/reference_narrow.py

The file is Pandoc's default reference doc with a page size and margins
added to the body's w:sectPr: an A4 page (11906 twips wide) with a 1800
twip left margin and a 1440 twip right margin, so its text width is 8666
twips. Pandoc's default w:sectPr has neither, and Word then shows a Letter
page with 1 in margins (9360 twips of text).
"""

import re
import subprocess
import zipfile
from pathlib import Path

OUT = Path(__file__).resolve().parent / "reference-narrow.docx"
PAGE = '<w:pgSz w:w="11906" w:h="16838"/>'
MARGINS = ('<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1800" '
           'w:header="720" w:footer="720" w:gutter="0"/>')


def main():
    default = subprocess.run(
        ["quarto", "pandoc", "--print-default-data-file", "reference.docx"],
        capture_output=True, check=True).stdout
    tmp = OUT.with_suffix(".tmp")
    tmp.write_bytes(default)
    with zipfile.ZipFile(tmp) as src, zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as out:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "word/document.xml":
                xml = data.decode("utf-8")
                # The body's own w:sectPr is the last one. Its only child,
                # w:footnotePr, comes before w:pgSz in schema order.
                end = xml.rindex("</w:sectPr>")
                xml = xml[:end] + PAGE + MARGINS + xml[end:]
                assert len(re.findall("<w:pgSz", xml)) == 1
                data = xml.encode("utf-8")
            out.writestr(info, data)
    tmp.unlink()


if __name__ == "__main__":
    main()
