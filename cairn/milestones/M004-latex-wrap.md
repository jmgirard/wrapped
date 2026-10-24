<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M004: Wrap figures in LaTeX PDF output

- **Status:** planned
- **Priority:** high
- **Depends on:** M002, M003
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes the PDF that users get from a wrapped figure
- **Branch/PR:** —

## Goal

A document rendered to PDF through LaTeX with the extension installed shows body text beside each figure marked `.wrap-left` or `.wrap-right`.

## Scope

**In:**
- `_extensions/wrapped/wrapped.tex`, the `wrappedfigure` wrapper from `spikes/s2/wrapped.tex`, with a gap key added. The filter loads it and wrapfig for LaTeX output (D-002).
- The filter sets `fig-env` and `fig-pos` for each wrapped float, and wraps the uncaptioned image in raw LaTeX. LaTeX leaves M002's format fallback.
- Width, gap, and line conversions, and the `wrapped:` metadata, for LaTeX.
- The knitr cell form on the LaTeX path (D-001), the caption that ran into the footer (spike S2), and the figure near a page break (E10).
- Two-column documents (E17) and `pdf-standard: ua-1` (E12).
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
- [ ] AC6: One fixture sets `classoption: twocolumn`, and one sets `classoption: [twocolumn]`. Each renders to PDF with exit status 0. In each, the wrapped figure is a `\begin{figure}` in the kept `.tex`, and the render prints one extension warning (E17). A fixture with `pdf-standard: ua-1` holds a wrapped captioned figure and a wrapped uncaptioned image, each with `fig-alt`. It renders to PDF with exit status 0. For each of the two, the structure tree of the PDF holds its alt text, or it renders as a normal figure with one extension warning (E12).
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

- [ ] T1: Copy the wrapper from `spikes/s2/wrapped.tex` to `_extensions/wrapped/wrapped.tex` and add a gap key that sets `\columnsep` inside the environment. Load it with `quarto.doc.include_file` and add wrapfig with `quarto.doc.use_latex_package`. Set `fig-env="wrappedfigure"` and `fig-pos` on each wrapped float for LaTeX. Remove LaTeX from the format fallback.
- [ ] T2: Convert the width (percent to a `\linewidth` fraction, px to pt), the gap, and the line count, with the metadata defaults. Wrap the uncaptioned image in a raw `wrappedfigure` that keeps its alt text.
- [ ] T3: Render the knitr cell form to PDF and confirm the moved class reaches LaTeX (D-001). Fix the caption that runs into the footer. Make the page-break figure keep its text beside it. Try wrapfig's floating placements (`R`, `L`) first.
- [ ] T4: Detect `twocolumn` in `classoption`, as a string or a list, and fall back with one warning. Render the ua-1 fixture and read the alt text from the PDF's structure tree. Fall back with a warning where the alt text is lost.
- [ ] T5: Add `.tex` snapshots for the fixtures to `tests/verify.py`. Make page images with `pdftoppm` and read them. Render the stop-rule and contexts fixtures to PDF. Write the LaTeX section of `README.md` with wrapfig's limits: lists, page breaks, figures in a row, two columns, narrowed headings, and the partial stop rule.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: question set: dependencies — wrapfig allowed as a LaTeX package that users' TeX distribution supplies. TinyTeX installs it on first use (D-002).
- 2026-10-24: criteria audit: see the M002 work log. The fixes here allow D-001's `#| wrap:` fallback, add the `\ref` and `??` checks, convert px to pt, limit the page-break promise to the planted figure, allow a ua-1 fallback, and render the stop-rule and contexts fixtures to PDF.
- 2026-10-24: the approach to the page-break figure is left to implement. wrapfig's floating placements are the first thing to try, because the S2 spike used the fixed placement and ran narrowed lines past the page break.

## Decisions

## Review
