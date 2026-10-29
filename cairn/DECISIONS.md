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

### D-012: The lone-shortcode stop looks past comments and one span, and a block-valued meta stops (supersedes part of D-011)

2026-10-28, M021. D-011's "exactly one shortcode and nothing else" now
means one shortcode with nothing else that shows: spaces, soft breaks, HTML
comments, and one span around it do not count. In HTML Quarto still
renders such a video as a block, and D-011 stops a video in every format.
A paragraph of one of the eight joining shortcodes with comments or a span
around it still joins, with one exception. D-011 let every lone `meta`
join; now a `meta` shortcode that is its paragraph's one inline stops
when its value holds a block other than a paragraph, because Quarto then
puts the value's blocks in the paragraph's place. The user chose at the
plan's question set that a value of paragraphs only joins, over stopping
at any block value, because paragraph text can wrap like typed text. A
`meta` in any other form keeps joining, because Quarto renders its value as
text there. The meta stop follows the value in each format, so a key set
for one format only stops in that format and joins in the others, where
Quarto renders it as text. The new stop forms are blocks of D-007's stop
rule and not paragraphs for D-003's next-block rule, as D-011's are.

### D-013: In a dashboard, a code cell outside a `.card` div keeps a normal figure

2026-10-28, M022. In a dashboard, a wrapped figure from a code cell that
is not inside a `.card` div keeps its normal layout with the warning "is
outside a card in a dashboard". Quarto's dashboard filter runs after this
filter and makes such a cell a card of its own, so the paragraphs after
the cell sit in another card, where no float can reach them. The user
chose, at the M021 plan's question set, a normal figure with a warning
where a float cannot work in a dashboard. The filter does not put the
cell and its paragraphs in a card for the user, because a card the user
did not write changes the dashboard's layout; the README asks the user to
write the `.card` div. A `.card` div that is itself a context, such as one
with `layout-ncol`, keeps that context.

### D-014: CI publishes the docs site with Quarto's publish action (extends D-008)

2026-10-28, M024. The user chose at the M024 plan's question set to add
`quarto-dev/quarto-actions/publish` to `.github/workflows/docs.yml`. On a
push to `main` or a manual run on `main`, it renders `docs/` and pushes the
site to the `gh-pages` branch, which GitHub Pages serves. The action comes
from Quarto's own organization, as the setup action of D-008 does, so it
adds no new publisher of CI code. A `gh-pages` branch was chosen over a
GitHub Actions Pages deploy because the branch can be published by hand
and checked live before the merge. On a pull request the workflow only
renders.

### D-015: After a small wrap-lines count, the stop block skips below the figure (annotates D-007)

2026-10-28, M025. D-007 skips space at the stop block only where the text
is still narrowed. A `wrap-lines` value smaller than the figure needs can
end the narrowed lines first, and then the stop block sat beside or over
the figure. The user chose at the M025 plan's question set to keep the
count for the narrowed lines and to move the stop block below the figure.
wrapfig documents a smaller count as its fix for vertical space that it
does not count, such as the space between paragraphs, so raising the count
to the height count was rejected. The skip compares positions on the page
where the wrap started, so it adds nothing after a page break or inside a
box such as a callout. The text inside the paragraphs past the count still
runs at full width, as wrapfig does.

### D-016: The docs workflow checks page layout with poppler and Playwright (extends D-008, D-014)

2026-10-29, M027. The user chose at the M027 plan's question set to run the
docs layout checks in `.github/workflows/docs.yml`. The render job installs
`poppler-utils` from Ubuntu's packages, as `verify.yml` does under D-008,
and Playwright for Python with its Chromium in a virtual environment. The
publish job waits for the render job, so a page that fails a check is not
published. Playwright was chosen over a script that drives the runner's own
Chrome because a maintained driver needs less custom code. The Word check
stays out of CI, because LibreOffice on Ubuntu uses other fonts than the
Mac and breaks lines in other places. D-005 still limits LibreOffice to
checks on the Mac. Playwright is a CI need and an option of
`tests/docs_layout.py` only. The test command in `tests/verify.py` does not
need it.

### D-017: In Word, the filter sets fig-alt as alt text only on figures it frames

2026-10-29, M029. Quarto 1.10.19 drops `fig-alt` from the Word alt text of
every captioned figure, wrapped or not. The user chose at the M029 plan's
question set to fix it for wrapped figures only, so a document that does
not use wrapping renders as Quarto renders it. A wrapped figure that keeps
a normal figure in Word, with a warning, is a normal figure under the
DESIGN.md goals, so it also keeps Quarto's alt text. Fixing every captioned
figure in Word was rejected because the filter would then change figures
that it does not wrap.

### D-018: In a Word frame, a float's fig-alt goes on its first image only (narrows D-017)

2026-10-29, M030. Quarto 1.10.19 copies a div float's `fig-alt` onto each
of its images, so a framed float with two images gave both the same alt
text. The user chose at the M030 plan's question set to put the float's
text on the frame's first image only. A later image keeps its own
`fig-alt`, or else the text in its square brackets, which is empty for
`![](x.png)`, so a screen reader reads the float's text once. An image's
own `fig-alt` wins on any image, the first included. Leaving the text on
neither image, as Quarto's HTML does, was rejected because the float's
`fig-alt` would then reach no reader in Word. Keeping it on every image was
rejected because a reader would hear it once per image.

### D-019: Triage drops four candidate rows as not worth keeping

2026-10-30, `/cairn-triage`. **Context:** a triage pass weighed every
candidate row and Known issues entry. Four rows cited no issue and no user
report, and each named an effect that only an undocumented input reaches
or that changes no output. **Decision:** the user accepted dropping them.
"Reject infinite widths and gaps": a width or gap with 310 or more digits
reads as inf, so Typst gets `infpt` and TeX rejects the dimension ("Dimension
too large"). "Check margins in slidy and other slides": in slidy, s5,
dzslides, and slideous, a `.column-margin` figure still warns "is in the
margin", where Quarto may not put it in a margin. "Name column widths in
Typst comments": the comments at `typst_open` and `TYPST_HEADER` in
`wrapped.lua` say "text width" where, with `columns:` set, the width is the
column width. "Correct the cancel comment in verify.yml": the comment says
runs on main are never cancelled, but a newer queued run replaces an older
queued one. **Consequences:** a later finding of the same effect is not
filed again unless a user reports it. Each drop can be reopened by an entry
that supersedes this one.
