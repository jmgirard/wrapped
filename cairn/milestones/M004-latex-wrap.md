<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M004: Wrap figures in LaTeX PDF output

- **Status:** in-progress
- **Priority:** high
- **Depends on:** M002, M003
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the PDF that users get from a wrapped figure
- **Branch/PR:** m004-latex-wrap

## Goal

A document rendered to PDF through LaTeX with the extension installed shows body text beside each figure marked `.wrap-left` or `.wrap-right`.

## Scope

**In:**
- `_extensions/wrapped/wrapped.tex`, the `wrappedfigure` wrapper from `spikes/s2/wrapped.tex`, with a gap key added. The filter loads it and wrapfig for LaTeX output (D-002).
- The filter sets `fig-env` and `fig-pos` for each wrapped float, and wraps the uncaptioned image in raw LaTeX. LaTeX leaves M002's format fallback.
- Width, gap, and line conversions, and the `wrapped:` metadata, for LaTeX.
- The knitr cell form on the LaTeX path (D-001), the caption that ran into the footer (spike S2), and the figure near a page break (E10).
- Two-column documents (E17) and tagged PDF with `pdf-standard: ua-2` (E12). Quarto 1.10.19 ignores `ua-1` for LaTeX.
- `.tex` snapshots in `tests/verify.py`, and a LaTeX section in `README.md` that states wrapfig's limits.

**Out:**
- Typst → the candidate "Wrap figures in Typst PDF output". Word → the candidate "Wrap figures in Word output with frames".
- A full stop rule in LaTeX. DESIGN says LaTeX enforces it only in part, because wrapfig measures its own height. The README states this.

## Acceptance criteria

- [ ] AC1: `quarto render tests/fixture.qmd --to pdf` with `keep-tex: true` exits with status 0. In the kept `.tex`, each captioned figure that the fixture wraps in HTML is in a `wrappedfigure` environment whose option names its side. The wrapped uncaptioned image is in one too. If the knitr form needs the `#| wrap:` cell option that D-001 names as the LaTeX fallback, the fixture's knitr figure uses it. The `.tex` holds a `\ref{fig-…}` for each `@fig-` link, and the PDF text from `pdftotext` holds no `??`.
- [ ] AC2: `pdftoppm` makes page images of the fixture's PDF. On them, each wrapped figure sits on its side, and lines of the paragraph after it sit beside it on the same page.
- [ ] AC3: The kept `.tex` shows six conversions. A percent `width` attribute becomes the matching fraction of `\linewidth`, so `40%` becomes `0.4\linewidth`. A `px` length becomes `pt` at 0.75 pt per px. Any other absolute length stays as it is. A `wrap-gap` value sets `\columnsep` for that figure only. A `wrap-lines` value becomes `lines=<n>`. In `tests/defaults.qmd`, a figure that sets neither attribute takes the `wrapped: width` and `wrapped: gap` metadata.
- [ ] AC4: The fixture places a wrapped figure with a caption of two or more lines near the bottom of a page. On the page images, the caption of each wrapped figure ends above the bottom edge of the text block. That edge is the lowest body line on a full page.
- [ ] AC5: The fixture holds two wrapped figures that start too near the bottom of a page to fit there. The first sets no `wrap-lines`, and the second sets it. On the page images, no page shows narrowed lines with no figure beside them for the first. The README states that `wrap-lines` can narrow lines past a page break.
- [ ] AC6: One fixture sets `classoption: twocolumn`, and one sets `classoption: [twocolumn]`. Each renders to PDF with exit status 0. In each, the wrapped figure is a `\begin{figure}` in the kept `.tex`, and the render prints one extension warning (E17). A fixture with `pdf-standard: ua-2` and `documentclass: article` holds a wrapped captioned figure and a wrapped uncaptioned image, each with its own `fig-alt` text. It renders to PDF with exit status 0. For each of the two, it is a `wrappedfigure` in the kept `.tex` and `pdfinfo -struct` lists a Figure tag with its `fig-alt` text, or it is a normal figure and the render prints one extension warning (E12). A copy of that fixture with `pdf-standard: ua-1` renders to PDF with exit status 0.
- [ ] AC7: `tests/stop-rule.qmd` and `tests/contexts.qmd` each render to PDF with exit status 0. In the kept `.tex` of the contexts fixture, no float that falls back in HTML is in a `wrappedfigure` environment.

## Coverage

- AC1 → T1, T2, T3, T5
- AC2 → T1, T5
- AC3 → T2, T5
- AC4 → T3, T5
- AC5 → T3, T5
- AC6 → T4, T5
- AC7 → T5

## Tasks

- [x] T1: Copy the wrapper from `spikes/s2/wrapped.tex` to `_extensions/wrapped/wrapped.tex` and add a gap key that sets `\columnsep` inside the environment. Load it with `quarto.doc.include_file` and add wrapfig with `quarto.doc.use_latex_package`. Set `fig-env="wrappedfigure"` and `fig-pos` on each wrapped float for LaTeX. Remove LaTeX from the format fallback.
- [x] T2: Convert the width (percent to a `\linewidth` fraction, px to pt), the gap, and the line count, with the metadata defaults. Wrap the uncaptioned image in a raw `wrappedfigure` that keeps its alt text.
- [x] T3: Render the knitr cell form to PDF and confirm the moved class reaches LaTeX (D-001). Fix the caption that runs into the footer. Make the page-break figure keep its text beside it. Try wrapfig's floating placements (`R`, `L`) first.
- [x] T4: Detect `twocolumn` in `classoption`, as a string or a list, and fall back with one warning. Render the ua-2 fixture and read the alt text from the PDF's structure tree with `pdfinfo -struct`; render a ua-1 copy. Fall back with a warning where the alt text is lost.
- [x] T5: Add `.tex` snapshots for the fixtures to `tests/verify.py`. Make page images with `pdftoppm` and read them. Render the stop-rule and contexts fixtures to PDF. Write the LaTeX section of `README.md` with wrapfig's limits: lists, page breaks, figures in a row, two columns, narrowed headings, and the partial stop rule.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: question set: dependencies — wrapfig allowed as a LaTeX package that users' TeX distribution supplies. TinyTeX installs it on first use (D-002).
- 2026-10-24: criteria audit: see the M002 work log. The fixes here allow D-001's `#| wrap:` fallback, add the `\ref` and `??` checks, convert px to pt, limit the page-break promise to the planted figure, allow a ua-1 fallback, and render the stop-rule and contexts fixtures to PDF.
- 2026-10-24: the approach to the page-break figure is left to implement. wrapfig's floating placements are the first thing to try, because the S2 spike used the fixed placement and ran narrowed lines past the page break.
- 2026-10-25: started; branch m004-latex-wrap cut from main at a40abc1.
- 2026-10-25: T1–T3 land in one commit, because the wrapper, the conversions, and the page-break handling share `wrapped.tex`, `wrapped.lua`, and the fixture.
- 2026-10-25: T1: wrapfig reads `\columnsep` when it places the figure at a later paragraph start, after the environment ends, so a `\columnsep` set inside the environment does nothing. The environment sets it globally at its end, and hooks on wrapfig's `\WF@startwrapping` and `\WFclear` restore the document's value once the figure is placed or put out.
- 2026-10-25: T1: options read `side=left|right`; the wrapper maps them to wrapfig's floating placements L and R. The wrapper also loads wrapfig itself, beside the filter's `use_latex_package`.
- 2026-10-25: T1: a new wrappedfigure first ends an earlier wrap whose text is still narrowed (skips the lines left, then `\WFclear`), because wrapfig cannot place a figure during another wrap. Without this, figures two paragraphs apart floated and collided in the fixture.
- 2026-10-25: T1: a moved figure that still waits for a paragraph when the next wrappedfigure starts is put out centered with no text, in place of wrapfig's left-edge dump.
- 2026-10-25: T1: defect found and fixed: unnumbered headings have no hanging indent, so wrapfig placed a moved figure at a heading, whose group then undid the wrap and the next text ran over the figure. The wrapper turns `\WF@floathand` off inside `\@hangfrom`.
- 2026-10-25: T1: captions inside wrappedfigure use the caption package's `format=plain, justification=raggedright`, because a hanging, justified caption in a 150px box spread its words apart.
- 2026-10-25: T2: TeX reads pt, pc, in, cm, mm, em, and ex as written. Any other CSS unit or a CSS function gives the default with a warning naming LaTeX; a metadata value LaTeX cannot use falls back to the built-in default with a warning. A wrapped image's width becomes `100%` (`\linewidth` of the box) and its height goes. `wrap-lines` that is not a whole number above 0 is dropped with a warning; HTML drops the attribute silently.
- 2026-10-25: T2: the lone image's raw wrappedfigure keeps the image a Pandoc Image. Pandoc writes no `alt=` for it outside ua-1 (seen in the kept `.tex`); T4 checks ua-1.
- 2026-10-25: T2: contexts, unplaced images and divs, and empty wrapped cells now warn in LaTeX as in HTML; LaTeX no longer prints the format warning.
- 2026-10-25: T3: the knitr cell's moved class reaches LaTeX: `fig-cell` is a wrappedfigure in the kept `.tex`, so D-001's `#| wrap:` fallback is not needed.
- 2026-10-25: T3: floating placement (R, L) fixes both S2 problems: a figure that does not fit moves to the next paragraph start. Planted figures `fig-bottom` (fits, caption ends about one line above the text block's bottom), `fig-break`, and `fig-break-lines` (both move to the next page) are at the end of `tests/fixture.qmd`, placed with raw `\clearpage` and `\vspace`.
- 2026-10-25: T3: fixture change: short sections got a second paragraph, and raw `\clearpage` blocks start the clamp and logo sections on a new PDF page, so each main figure fits beside its first paragraph. Before that, the clamp figure moved and was put out with no text, and the logo figure sat beside its second paragraph.
- 2026-10-25: T5 part: `tests/verify.py` renders `defaults` to PDF, and the `.tex` snapshot now records each environment's options and reads only the document body. `verify.py` renders `fixture` to Typst after LaTeX, so the `fixture.pdf` left on disk is Typst's; page images need a separate `--to pdf` render.
- 2026-10-25: substantive amendment: AC6, Scope In, and T4 move the tagged-PDF check from `ua-1` to `ua-2` with `documentclass: article`. Quarto 1.10.19 prints "PDF standard 'ua-1' is not supported by LaTeX and will be ignored" and makes no structure tree, with or without the extension; `ua-2` with the default scrartcl fails ("\DocumentMetadata not supported!") with or without it. The extension's behavior is unchanged, so no stop.
- 2026-10-25: re-audit: AC6 (full) — first branch did not require the item to stay wrapped; the ua-1 exit-0 render was dropped; no named procedure for the structure tree; Scope and T4 still said ua-1. All four fixed in the wording above.
- 2026-10-25: re-audit: AC6 (full) — the fallback branch does not check alt text; "one extension warning" does not name the warning or the total; plant more `classoption` forms; README should say ua-1 gives no tags. Answered, no wording change (a third change would be a stop): both ua-2 items take the `wrappedfigure` branch with their alt text (`pdfinfo -struct` lists "A scatter plot of ten rising points" and "A small scatter plot"), so the fallback branch is not exercised; the snapshots pin each warning's exact text and count; plants `[a4paper, twocolumn]` and `twocolumn,10pt` each printed one two-column warning and kept `\begin{figure}`, and `onecolumn` wrapped with no warning; the README note goes in T5.
- 2026-10-25: T4: the wrapped uncaptioned image takes its `fig-alt` as its description, so Pandoc writes `alt=`; without this its tag read "plot.png", as it does with no extension, because Quarto writes `fig-alt` only for figures. Fixtures `twocolumn`, `twocolumn-list`, `pdf-ua`, `pdf-ua1`, and PDF renders of `contexts` and `stop-rule` joined `verify.py` with snapshots (21 renders pass).
- 2026-10-25: T5: README gains a "PDF through LaTeX" section (conversions, `wrap-lines`, ragged-right captions, the limits list, tagged PDF) and LaTeX mentions in the stop, context, and notes sections. Each limit was seen this session: stop-rule PDF pages show headings, lists, and quotes narrowed beside the figure and a heading narrowed after a page break; a probe with `wrap-lines="30"` ran narrowed lines onto the next page; the centered fallback showed in a fixture iteration. DESIGN's syntax note and architecture passes now name the LaTeX path.

## Decisions

## Review
