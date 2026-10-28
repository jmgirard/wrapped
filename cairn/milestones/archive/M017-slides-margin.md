# M017: Let slides wrap under margin settings

**Status:** done (2026-10-28, PR #18 https://github.com/jmgirard/wrapped/pull/18)

**Goal:** On revealjs slides, a wrapped figure that a margin class or a document margin value names wraps, because slides have no margin column.

**Outcome:** `margin_context` in `wrapped.lua` names no place for `column-margin` and `fig-column-margin` when the new `is_revealjs` flag is set (also used by `has_page_layout`), so every margin path on slides wraps: a float's own class, a margin div, `#| column: margin` and `#| fig-column: margin` cells, a captioned image with no id or an image with the class, and a document `fig-column: margin` or `column: margin` through `read_meta`. An `.aside` still keeps the figure normal with an "is in an aside" warning, since the theme sets an aside at the slide's foot by default. Fixtures: nine cases added to `tests/revealjs.qmd` (two knitr cells), new `revealjs-margin-meta` and `revealjs-column-margin` (97 renders). README "Slides" and the margin item of "Where a figure keeps its normal layout", DESIGN steps 2 and 4, E3, E15, and E21 updated.

**Decisions:** none.

**Review:** All 4 criteria verified; 97 renders green locally, and AC4's CI half passed in the verify workflow on PR #18 (5m36s) before the merge. Claim audit: 19 claims, 3 narrowed to "by default" for the aside and re-read once. Four-lens review, 26 findings: 11 fixed (no fixture for the no-id and bare image paths; README fallback list, DESIGN steps 2 and 4, E21, and two code comments missed the slide rule), 13 rejected, 2 follow-up. Hygiene: row "Let slides wrap under margin settings" graduated; new rows "Let asides wrap on centered slides" and "Check margins in slidy and other slides"; M014 row pruned; one lesson captured; lesson 2026-10-26 (M007) on `\vspace*` probes for LaTeX faults evicted by rank; lesson 2026-10-27 (M015) on bare renders marked used.
