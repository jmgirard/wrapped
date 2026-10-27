# M014: Keep two-figure cells unwrapped

**Status:** done (2026-10-27, PR #14 https://github.com/jmgirard/wrapped/pull/14)

**Goal:** A code cell with a wrap class that makes more than one figure without `fig-subcap` keeps all its figures in their normal layout in every format, with one warning for the cell (D-010).

**Outcome:** `cell_div` sets `several` on the carry when `count_top_floats` finds more than one float that sits in no other float. `float_target` then keeps each figure of the cell normal through the new `keep_normal` helper, before `clean_images`, and prints one warning at the first figure: "the code cell #<label> makes more than one figure, so it does not wrap.", the label being the float id less its `-N` ending. The context branch and the next-block branch run first, so a cell in a context keeps its per-figure warnings and a cell with no paragraph after it prints none. A `fig-subcap` cell (one float with subfloats) and a `layout-ncol` cell keep their panel warnings. New contexts.qmd cells: fig-two-plots, fig-three-plots, fig-two-subcap, fig-two-before-heading (76 renders). README "Where a figure keeps its normal layout" and the next-block paragraph name the case; DESIGN.md Goals, the next-block note, and Architecture step 4, and wrap-mechanisms E4 and E7 follow D-010.

**Decisions:** D-010 (narrows D-003 for the figures of one cell). The question set chose all figures normal with one warning over D-003's second-one-wraps and over stacking the figures on one side.

**Review:** All 5 criteria verified, the suite green locally (76 renders) and in CI (verify, 5m31s). Criteria audit at plan: 6 findings, all fixed. Claim audit: 11 claims read, 2 corrected. Four-lens review, 23 findings: 14 fixed (the no-paragraph fixture, README layout-option and own-cell wording, next-block paragraph, E7, DESIGN.md Goals and step 4, three code comments, keep_normal helper), 9 rejected plus one part (2 edge: a cell mixing a table float and a figure float), 0 follow-up. Hygiene: row "Handle a wrapped cell with two figures" graduated; M011 row pruned; one lesson captured; lesson 2026-10-25 (M005) on Typst `lang` and `dir` evicted by rank; six lessons marked used.
