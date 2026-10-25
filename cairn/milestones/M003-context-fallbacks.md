<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M003: Fall back in contexts that cannot wrap

- **Status:** review
- **Priority:** high
- **Depends on:** M002
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes what users see for wrapped figures in margins, lists, callouts, tables, books, and slides
- **Branch/PR:** m003-context-fallbacks

## Goal

Wrapped figures render as the research page's edge cases E3 to E8, E13, and E15 state, with E7 as D-003 states.

## Scope

**In:**
- Context detection in `wrapped.lua`. A wrapped float in a margin, an aside, a subfigure panel, a table float, a list, a callout, a column layout, or a tabset keeps its normal layout. Each such float prints one warning that names its id.
- The next-block rule. A wrapped figure whose next block is not a paragraph keeps a normal figure with no warning (E6, and the first figure of E7 as D-003 states).
- A contexts fixture, a two-chapter book fixture, and a revealjs fixture, all covered by `tests/verify.py`.
- README updates for the contexts that keep a normal figure and for revealjs.

**Out:**
- What LaTeX does with these fixtures → M004, which renders them to PDF.
- Other margin forms, such as `cap-location: margin` and `.column-page`, and nested or ordered lists → no milestone yet. A later plan adds them if users report them.

## Acceptance criteria

- [ ] AC1: `tests/contexts.qmd` renders to HTML. It holds a wrapped float in each of the nine forms below, and the promise covers those forms. The E3 forms are a `.column-margin` figure, a figure in a `.aside` div, and a knitr cell with `#| column: margin`. The E4 form is a subfigure panel with `layout-ncol`, and the E5 form is a `#tbl-` float. The E8 forms are a bullet list item, a `callout-note`, a `.columns` layout, and a tabset. In the output, none of these floats carries a `wrap-left` or `wrap-right` class. For each one, the terminal output holds one extension warning that names the float's id. Each E3 figure sits in the same margin container as in a render of the same file without the extension.
- [ ] AC2: In the same fixture, a wrapped figure is the last block before a heading. It renders without a wrap class, and no warning names its id (E6).
- [ ] AC3: In the same fixture, two wrapped figures follow each other with no paragraph between them, and paragraphs follow the second. The first renders without a wrap class, and no warning names its id. The second keeps its wrap class. In the browser at 1200 px, the paragraph after the second sits beside it (E7, as D-003 states).
- [ ] AC4: A two-chapter book fixture renders to HTML with exit status 0. The wrapped figure in chapter 1 carries its wrap class. In chapter 2, the `@fig-` link to it is an `<a>` whose `href` ends with that figure's id (E13).
- [ ] AC5: `tests/revealjs.qmd` holds one slide with a wrapped figure and a paragraph after it. It renders with exit status 0. In the browser at a 1050 by 700 px viewport, the figure floats to its side by computed `float`, and the first line of the paragraph sits beside it. The README shows the revealjs case (E15).

## Coverage

- AC1 → T1, T3
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T3
- AC5 → T3, T4

## Tasks

- [x] T1: Context detection in `wrapped.lua`. Track the enclosing list, callout, column layout, tabset, aside, and margin block in the top-down pass. Detect subfigure panels and `#tbl-` floats. Remove the wrap class from each such float and print one warning that names its id. Leave the margin classes as Quarto sets them.
- [x] T2: The next-block rule. When the block after a wrapped figure is not a paragraph, remove the wrap class with no warning.
- [x] T3: Write `tests/contexts.qmd`, a two-chapter book under `tests/book/`, and `tests/revealjs.qmd`. Add them to `tests/verify.py` with snapshots.
- [x] T4: Check the revealjs layout in the built-in browser and adjust `wrapped.css` for slides if needed. Update `README.md` with the contexts that keep a normal figure and with the revealjs case.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: question set: back-to-back wrapped figures — the first falls back with no warning and the second wraps (D-003). The research page's E7 row is corrected to match.
- 2026-10-24: criteria audit: see the M002 work log. The fixes here name the float's id, compare the margin container with a render without the extension, add the knitr margin cell, and fix the revealjs viewport.
- 2026-10-24: a context fallback warns once for each float and names its id. A format fallback (M002) warns once for each render. The research page's "One warning" for each edge case and "warns once per document" for W5 support this reading.

- 2026-10-25: started by /milestone-implement on branch m003-context-fallbacks.
- 2026-10-25: T1 done. A `find_contexts` pre-pass marks floats in a list, callout, column layout, tabset, aside, margin block, or subfigure panel by custom id, because the float pass has no exit hook to track an enclosing block. The float pass also falls back for a table, a float's own margin class, and a `layout` attribute. Context warnings print in HTML only, like the other per-figure warnings. Choices: ordered lists count as lists; a captioned image with no id and a lone image in a context also fall back with a warning; the outermost context names the warning. The main fixture's snapshot gains the `#tbl-cars` warning (E5).
- 2026-10-25: T2 done. A `find_no_text` pre-pass records floats and cell floats whose next block, past comments, is not a joining paragraph, and strips the class from a no-id figure or lone image there. It skips lists inside a code cell or float, where the figure is the last block by design (a first version broke the main fixture's cell figure). The contexts fixture gains a no-id figure and a lone image, each in a context and before a heading.
- 2026-10-25: T3 done. `verify.py` now renders 14 fixtures: `contexts.html`, the `tests/book/` project (chapters `index.qmd` and `two.qmd`, with `_extensions` and `plot.png` links), and `revealjs.revealjs`. A folder fixture renders as a project and its snapshot lists each page plus xref hrefs. For `contexts`, the script renders a no-filter copy and records whether each E3 figure keeps the same column-margin container; all three do. Snapshots now list `tbl-` floats and read revealjs's `data-src`; the main fixture gains a `tbl-cars` line.
- 2026-10-25: T4 done. Built-in browser, `tests/layout.js`: revealjs slide at 1050x700, `#fig-slide` computed float right, first line at x=53 y=126 beside the box (620–998, top 115), all checks ok; contexts page at 1200, `#fig-second` float right, first line beside, fallback figures float none; main fixture all 12 figures ok. Fixes: `wrapped.css` sets `max-width: 100%` on wrapped images (revealjs caps images at 95%); `layout.js` scales the computed margin to screen px for scaled slides. A scratch render for the README claims found a panel with no wrap class warning because `image_wrap` read a subfigure's image; it now skips nested floats, and the contexts fixture gains `#fig-plain-panel` as its regression case. README gains the next-block rule, the contexts that keep a normal layout, and a Slides section.
- 2026-10-25: delegation: claim audit to a fresh Opus reader. It could not open the local server in the browser pane, so the `layout.js` scale comment rests on its code read and on this session's browser run (gap 40 to 36 px after the change).
- 2026-10-25: claim audit: 54 claims read, 3 corrected — README.md, tests/verify.py
- 2026-10-25: all tasks done; verify passes (14 renders). Status set to review.

## Decisions

## Review
