"""Write the Word reference docs that the docx fixtures read.

Run from the repository root:

    python3 tests/reference_narrow.py

Each file is Pandoc's default reference doc with settings added to the
body's w:sectPr. Pandoc's default w:sectPr holds only w:footnotePr, and
Word then shows a Letter page with 1 in margins (9360 twips of text).

- tests/reference-narrow.docx, for docx-reference.qmd: an A4 page (11906
  twips wide) with a 1800 twip left margin and a 1440 twip right margin,
  so its text width is 8666 twips.
- tests/reference-gutter.docx, for docx-options.qmd: a Letter page (12240
  twips wide) with 1440 twip margins and a 720 twip gutter, so its text
  width is 8640 twips.
- tests/reference-columns.docx, for docx-columns.qmd: two columns.
"""

import re
import subprocess
import zipfile
from pathlib import Path

TESTS = Path(__file__).resolve().parent
PAGE = '<w:pgSz w:w="11906" w:h="16838"/>'
MARGINS = ('<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1800" '
           'w:header="720" w:footer="720" w:gutter="0"/>')
GUTTER = ('<w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" '
          'w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="720"/>')
COLUMNS = '<w:cols w:num="2" w:space="720"/>'
FILES = {
    "reference-narrow.docx": PAGE + MARGINS,
    "reference-gutter.docx": GUTTER,
    "reference-columns.docx": COLUMNS,
}


def write(default, out, settings):
    tmp = out.with_suffix(".tmp")
    tmp.write_bytes(default)
    with zipfile.ZipFile(tmp) as src, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "word/document.xml":
                xml = data.decode("utf-8")
                # The body's own w:sectPr is the last one. Its only child,
                # w:footnotePr, comes before these settings in schema order.
                end = xml.rindex("</w:sectPr>")
                xml = xml[:end] + settings + xml[end:]
                assert len(re.findall("<w:sectPr", xml)) == 1
                data = xml.encode("utf-8")
            dst.writestr(info, data)
    tmp.unlink()


def main():
    default = subprocess.run(
        ["quarto", "pandoc", "--print-default-data-file", "reference.docx"],
        capture_output=True, check=True).stdout
    for name, settings in FILES.items():
        write(default, TESTS / name, settings)


if __name__ == "__main__":
    main()
