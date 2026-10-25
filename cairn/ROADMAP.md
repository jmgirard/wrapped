# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-10-25 (M004 done: HTML and LaTeX core row graduated, M001 row pruned, two LaTeX follow-up rows added, three lessons captured)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->
| M005 | Wrap figures in Typst PDF output | review | — | high | milestones/M005-typst-wrap.md |
| M004 | Wrap figures in LaTeX PDF output | done | M002, M003 | high | milestones/archive/M004-latex-wrap.md |
| M003 | Fall back in contexts that cannot wrap | done | M002 | high | milestones/archive/M003-context-fallbacks.md |
| M002 | Wrap figures in HTML output | done | — | high | milestones/archive/M002-html-wrap.md |

## Candidates
<!-- unnumbered ideas; one line each, ordered high → normal → low → parked:
     - [high] short title: detail — added YYYY-MM-DD — links
     - short title: detail — added YYYY-MM-DD — links
     - [parked] short title: detail; promote when <condition> — added YYYY-MM-DD — links
     the opening token is `[high]`/`[low]`/`[parked]` or absent (`normal`); `[parked]` marks a row whose
     promotion condition has not held — tracking-rules "Candidate priority token";
     open each row with its short title, the words the cairn pane shows, then `: `;
     the title is one sentence with no ending period, at least 5 words and at most 40 characters,
     ending with `(#N)` for a row written for GitHub issue N, such as
     `Fix SE of skewness calculation (#100)`; `/cairn-triage` offers a new title for one
     with fewer than 5 words or more than 40 characters; tracking-rules "Candidate short title" has the whole rule -->
- Wrap figures in Typst PDF output: W3, with wrap-it bundled under `typst/packages`. Spike S3 in M001 showed that wrap-it 0.1.1 renders wrapped text with a citation. Add a `@citation` in wrapped text to `tests/fixture.qmd`, as the research page's test plan asks (M002 review, ripple #4) — added 2026-10-24 — references/wrap-mechanisms.md — started M005
- Wrap figures in Word output with frames: W4. Spike S4 in M001 showed that Word opens the file and shows one merged frame. This work also checks how LibreOffice and Google Docs show the frame (moved from M001 on 2026-10-24), and shows Word the frame `w:pPr` in the order a filter makes, after Pandoc's own `w:pPr`, with the caption style checked (found at M001 review) — added 2026-10-24 — references/wrap-mechanisms.md
- Honor wrap-clear and figures in LaTeX: in PDF through LaTeX, a figure with no wrap class in the lines beside a wrapped figure overlaps its caption (stop-rule case 8), and a `wrap-clear` div does nothing. The wrapper's end-of-wrap step (skip the lines left, then `\WFclear`) could run before such a figure and at a `wrap-clear` div. That skip also follows `wrap-lines`, so a large value leaves blank lines before the next wrapped figure (M004 review, diff-bug #8). Found by the M004 claim audit — added 2026-10-25 — milestones/M004-latex-wrap.md
- Detect two-column LaTeX classes and gaps: the filter reads only `classoption`, so a class that is two-column by default (IEEEtran, acmart sigconf, revtex) or a `\twocolumn` in a header gets wrapfig figures with no warning. `wrapped.tex` sets `\columnsep` globally while a moved figure waits, so a `multicols` that starts then, or a column page shipped then, takes the figure's gap, and a local `\columnsep` around a wrappedfigure leaks out on restore. Found at M004 review (diff-bug #1, #3) — added 2026-10-25 — milestones/M004-latex-wrap.md
- Handle a wrapped cell with two figures: a code cell with `#| classes: wrap-right` that makes two figures floats both side by side in HTML. Decide whether such a cell wraps its first figure, falls back with a warning, or joins the subfigure fallback (E4). Found at M002 review (diff-bug #5, blame-history #3). A cell with `fig-subcap` or `layout-ncol` now keeps a normal panel with a warning (M003). In Typst both figures go in one box with the first figure's side and width (M005 review, blame-history #3) — added 2026-10-24, narrowed 2026-10-25 by M003 review — milestones/M002-html-wrap.md
- Check wrapped figures in dashboards: in a Quarto dashboard the `.wrap-group` div likely gets `html-fill-container`, a flex container, where a float has no effect. Not verified. Make wrapping work there or fall back with a warning. Found at M002 review (diff-bug #9) — added 2026-10-24 — milestones/M002-html-wrap.md
- Fall back in other margin and list forms: a cell with `#| fig-column: margin` floats inside the margin with no warning, and a figure in a loose definition list wraps. `cap-location: margin` and `.column-page` are untested. M003 left these out of scope (M003 review, diff-bug #4 and #6). In Typst a figure in a definition list or a table cell wraps too, and a call in a table cell is indented, so the `.typ` summary does not read it (M005 review pass 2, diff-bug #4) — added 2026-10-25 — milestones/archive/M003-context-fallbacks.md
- Bound wide absolute widths in Typst: a wrapped figure whose absolute width, such as `7in`, is as wide as the text column or wider leaves no room for the text in wrap-it's grid, and the text can drop from the PDF with no warning. The filter cannot know the text width, so a check would run in Typst. Percents of 100% or more are handled in M005 (M005 review, diff-bug #2) — added 2026-10-25 — milestones/M005-typst-wrap.md
- Warn when a figure width is zero: `width="0%"` passes the length checks, and in Typst it gives an empty box and a caption broken into a zero-width column with no warning; HTML takes the same value (M005 review pass 2, diff-bug #5) — added 2026-10-25 — milestones/M005-typst-wrap.md
- Check wrapped figures in Typst columns: a Typst document with `columns:` set puts the text in columns, and no one has tested a `wrap-content` call there. Make wrapping work there or keep a normal figure with a warning, as LaTeX does for two columns. Left out of M005 — added 2026-10-25 — milestones/M005-typst-wrap.md
- Check CSS function lengths before use: `css_length` passes any `calc()`, `min()`, `max()`, or `clamp()` text unread, so `width="calc(banana)"` or `breakpoint: calc(50%)` reaches the CSS with no warning (M003 review, prior-review #1; same class as M002 review pass 1 finding 7) — added 2026-10-25 — milestones/archive/M003-context-fallbacks.md
- Run the fixture renders in CI: a GitHub Actions workflow that runs `tests/verify.py` against the Quarto release and pre-release channels, with TinyTeX and R with knitr installed (research page, test plan). Chosen for later at the M002 plan's question set — added 2026-10-24 — references/wrap-mechanisms.md
- [low] Use the HTML stylesheet for EPUB: EPUB is HTML-based, so the W1 stylesheet can apply there. Version 1 keeps a normal figure in EPUB (W5) — added 2026-10-24 — references/wrap-mechanisms.md
