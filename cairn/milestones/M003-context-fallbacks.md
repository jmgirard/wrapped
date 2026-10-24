<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M003: Fall back in contexts that cannot wrap

- **Status:** planned
- **Priority:** high
- **Depends on:** M002
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — it changes what users see for wrapped figures in margins, lists, callouts, tables, books, and slides
- **Branch/PR:** —

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

- [ ] T1: Context detection in `wrapped.lua`. Track the enclosing list, callout, column layout, tabset, aside, and margin block in the top-down pass. Detect subfigure panels and `#tbl-` floats. Remove the wrap class from each such float and print one warning that names its id. Leave the margin classes as Quarto sets them.
- [ ] T2: The next-block rule. When the block after a wrapped figure is not a paragraph, remove the wrap class with no warning.
- [ ] T3: Write `tests/contexts.qmd`, a two-chapter book under `tests/book/`, and `tests/revealjs.qmd`. Add them to `tests/verify.py` with snapshots.
- [ ] T4: Check the revealjs layout in the built-in browser and adjust `wrapped.css` for slides if needed. Update `README.md` with the contexts that keep a normal figure and with the revealjs case.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: question set: back-to-back wrapped figures — the first falls back with no warning and the second wraps (D-003). The research page's E7 row is corrected to match.
- 2026-10-24: criteria audit: see the M002 work log. The fixes here name the float's id, compare the margin container with a render without the extension, add the knitr margin cell, and fix the revealjs viewport.
- 2026-10-24: a context fallback warns once for each float and names its id. A format fallback (M002) warns once for each render. The research page's "One warning" for each edge case and "warns once per document" for W5 support this reading.

## Decisions

## Review
