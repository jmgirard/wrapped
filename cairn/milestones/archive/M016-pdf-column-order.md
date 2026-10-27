# M016: Read figure columns in Quarto's order in PDF

**Status:** done (2026-10-28, PR #17 https://github.com/jmgirard/wrapped/pull/17)

**Goal:** In PDF through LaTeX and PDF through Typst, a wrapped figure keeps its normal layout for its column only where Quarto 1.10.19 puts it in the margin or a page-wide column.

**Outcome:** `column_context` in `wrapped.lua` reads a float's column in LaTeX and Typst in Quarto's order (own `fig-column-*`, document `fig-column`, own `column-*` or `aside`, document `column`) and returns whether the document's value decided, which `float_target` reads after a layout attribute, as HTML and Word do. `read_meta` sets `meta_fig_column_set` and `meta_column_set`; `block_context` skips a code cell's own column class in LaTeX and Typst when the document sets either key. HTML and Word keep their rule. Fixtures: new column-order, column-order-page, column-order-fig-margin, column-order-margin (LaTeX and Typst, 95 renders). README "Where a figure keeps its normal layout" (the order list), DESIGN steps 2 and 4, and E3, E21 updated.

**Decisions:** none milestone-local. The plan split the three margin follow-up rows into M016, M017, and M018 after the criteria audit found bare HTML renders do not show Quarto's order, so this milestone covers PDF only.

**Review:** All 3 criteria verified; 95 renders green locally and in CI (verify, 7m31s). Criteria audit: 11 findings on the one-milestone draft, all disposed by narrowing. Claim audit: 16 claims, 1 corrected and re-read once. Four-lens review, 28 findings: 18 fixed (a cell that writes its own `.column-margin` figure lost the class; a panel under a document key warned page-wide in Typst; README, DESIGN, E3, E21, and comment wording), 8 rejected, 2 follow-up. Hygiene: row "Read fig-column over a figure's class" graduated; new rows "Check HTML column order in a browser", "Wrap no-id margin images in PDF", "Read cell images by column order in PDF"; M013 row pruned; one lesson captured; lesson 2026-10-25 (M002, used M007) on a `FloatRefTarget` inside a new Div evicted by rank; four lessons marked used.
