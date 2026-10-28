# Decisions

Append-only. Never renumber; supersede with a new entry. D-entries record
choices with rationale — never deferrals ("not now" is a ROADMAP fact).

### D-001: Code-cell figures keep `#| classes:`, and the filter reads the cell div

2026-10-24, M001. For a figure from a knitr or Jupyter cell, the planned
syntax `#| classes: wrap-right` stays. The filter carries the class from the
cell's enclosing div to the figure in a top-down pass. It does not switch to a
`#| wrap: right` cell option. DESIGN.md had named that option as the fallback
if `classes` did not reach the figure node. Spike S1 showed that the class
does not reach the node but does reach the enclosing cell div for both
engines. A top-down pass sees that div before the figure, and a class it
adds to the figure reaches the HTML figure div. The existing syntax
therefore works, and a second cell option gives users two ways to say one
thing. The LaTeX path for a moved class is not tested. If it fails there,
the `#| wrap:` option comes back as the fallback for that path. Evidence:
`references/wrap-mechanisms.md`, S1.

### D-002: Dependencies for the HTML and LaTeX core

2026-10-24, plan of M002 to M004. The user allowed these dependencies at the
plan's question set. The extension uses the LaTeX package wrapfig for PDF
through LaTeX. Users' TeX distribution supplies it, and TinyTeX installs it
on first use. wrapfig is the package that spike S2 tested, and LaTeX has no
built-in way to wrap text. The test command in `tests/verify.py` needs R
with knitr and TinyTeX, because the fixture renders a knitr cell and a PDF.
The Jupyter cell form stays out of the test command, because the system
Python has no Jupyter. It gets one check by hand in a throwaway environment,
as spike S1 did. Spike S1 showed the same class placement for both engines.

### D-003: Back-to-back wrapped figures: the first falls back, the second wraps

2026-10-24, plan of M003. This replaces edge case E7 in
`references/wrap-mechanisms.md`, which said that the second figure falls
back with a warning. Under the stop rule, a figure whose next block is not a
paragraph has no text to wrap. The first of two back-to-back figures is such
a figure, so it keeps a normal figure with no warning, as E6 does for a
figure before a heading. The second figure has paragraphs after it, so it
wraps them. The user chose this at the plan's question set over keeping E7
as written and over a fallback for both figures.

### D-004: Bundle wrap-it 0.1.1 for PDF through Typst

2026-10-25, plan of M005. The user allowed this dependency at the plan's
question set. The extension ships a copy of the Typst package wrap-it 0.1.1,
with its license, under `_extensions/wrapped/typst/packages/preview/`, and
Quarto 1.9.36 or later loads it from there. Typst has no built-in way to wrap
text around a figure. Spike S3 showed that wrap-it renders a citation and a
`@fig-` link in the text beside a figure. A bundled copy needs no download at
render time. wrap-it's Unlicense allows the copy. meander was the other
choice. It lays out whole pages, so it does not fit a figure placed between
two blocks.

### D-005: LibreOffice as a check tool for Word output

2026-10-25, plan of M006. The user allowed this tool at the plan's question
set. LibreOffice, installed with `brew install --cask libreoffice`, converts
a test docx to PDF with no window (`soffice --headless --convert-to pdf`),
so its view of a Word frame can be read from page images. It is used for
the README's record of what each app shows and for review checks, not in
the test command in `tests/verify.py`, which keeps the needs that D-002
names. Word checks use the Microsoft Word already on the Mac, through
AppleScript. Google Docs is checked by the user's own look.

### D-006: poppler as a test requirement for LaTeX layout

2026-10-26, plan of M007. The user allowed this tool at the plan's question
set. The test command in `tests/verify.py` reads word and image positions
from the PDFs that it renders through LaTeX with poppler's command-line
tools (`pdftotext`, `pdftohtml`), installed with `brew install poppler`, and
fails with a plain message when they are missing. This adds poppler to the
needs that D-002 names. A position read is the one check that sees where a
stop block starts beside a figure, and the `.tex` snapshot shows only where
the filter puts a command. The user chose it over a position log that TeX
writes from a header that only a test file loads, which needs more test
code and depends on the PDF engine, and over page images checked by eye,
which no test fails on.

### D-007: LaTeX wraps end at the stop block, a waiting figure included (corrects D-006)

2026-10-26, M007, narrowing M004's LaTeX behavior. The user chose at the
M007 plan's question set that PDF through LaTeX ends a wrap at every block
that the stop rule names, as HTML, Typst, and Word do, over ending it only
at a `wrap-clear` div and before an unwrapped figure. The filter writes
`\wrappedstop` after each group's last paragraph. Where the wrap is still
narrowed, it skips the lines that the figure's height still needs. The plan
then chose, as a consequence of that answer, how a waiting figure ends: a
figure that moved because it did not fit and still waits for a paragraph
is put out there with no text beside it, before the stop block. Under M004
such a figure waited for any later paragraph on its group level, which
could put it beside text after a heading that is not its own. The cost is
that a figure near a page's end wraps less often: when its paragraphs end
before it can be placed, it renders centered with no text beside it. A
`wrap-lines` value now sets the most lines beside a figure, since a stop
block can end the wrap before that count.

This entry also corrects D-006: the test command reads positions with
poppler's `pdftohtml` alone, not `pdftotext`, because `pdftohtml -xml` also
gives image boxes. Poppler joins the test command's needs beside those that
D-002 names, which D-005 kept unchanged for LibreOffice.

### D-008: CI tools for the test command

2026-10-26, plan of M008. The user chose at the plan's question set to run
`tests/verify.py` in GitHub Actions. The workflows run on an Ubuntu runner
and use `actions/checkout`, `quarto-dev/quarto-actions/setup` (Quarto and
TinyTeX, from Quarto's own organization), `actions/upload-artifact`, and the
Ubuntu packages `r-base`, `r-cran-knitr`, `r-cran-rmarkdown`, and
`poppler-utils`. These install the needs that D-002 and D-006 name and add
none to the test command itself. Ubuntu packages were chosen over
`r-lib/actions/setup-r` so that Quarto's action is the only third-party
action. The user chose that Quarto's pre-release channel only reports: it
runs weekly and by hand, never on a pull request, so its failure blocks no
merge.

### D-009: CI installs R from binaries with r-lib's actions (supersedes part of D-008)

2026-10-26, M008 review. The user chose at the re-posed merge question to
replace the Ubuntu packages `r-base`, `r-cran-knitr`, and
`r-cran-rmarkdown` with `r-lib/actions/setup-r` (R with Posit's public
package manager) and `r-lib/actions/setup-r-dependencies` (knitr and
rmarkdown as binaries). Ubuntu's package mirror made the install step's
time vary from seconds to more than half an hour across runs, close to the
job timeout, so a slow mirror could fail a pull request that changed
nothing. D-008 chose the Ubuntu packages to keep Quarto's action the only
third-party action; that reason no longer outweighs the install time.
`poppler-utils` stays an Ubuntu package. The rest of D-008 stands.

### D-010: A wrapped code cell with more than one figure keeps them all normal (narrows D-003)

2026-10-27, plan of M014. A code cell with a wrap class that makes two or
more figures without `fig-subcap` keeps every one of its figures in the
normal layout, in every format, and the render prints one warning for the
cell. D-003's rule for back-to-back figures, where the first keeps a normal
figure and the second wraps, does not apply to the figures of one cell. The
user chose this at the plan's question set over D-003's rule and over
stacking the figures on one side. One rule holds in all four formats, and
LaTeX's wrapfig and a Word frame each hold one figure, so a stack would
need its own fallback there.

### D-011: A paragraph with a lone shortcode stops a wrap unless the shortcode is one of eight that join (annotates D-003, D-007)

2026-10-28, plan of M020. A paragraph that holds exactly one shortcode and
nothing else ends a wrap group in every format, unless the shortcode is
one of eight Quarto shortcodes that usually make text, an image, or
paragraphs: `meta`, `var`, `env`, `kbd`, `lipsum`, `placeholder`,
`version`, and `brand`. Such a paragraph is one of the blocks the stop rule
names for D-007, and it is not a paragraph for D-003's next-block rule.
The user chose at the plan's question set to stop at every shortcode that
is not known to join, over stopping only at known block shortcodes
(`pagebreak`, `video`, `contents`). The filter runs before shortcodes
render, so it cannot see what an unknown shortcode makes. A block beside a
float can overlap the figure, while an early stop only leaves space. The
user also chose that a `video` stops the wrap in every format, though it is
a block only in HTML, so the stop rule stays the same in all formats.
