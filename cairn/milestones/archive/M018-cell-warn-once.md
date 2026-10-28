# M018: Warn once per cell under a context

**Status:** done (2026-10-28, PR #19 https://github.com/jmgirard/wrapped/pull/19)

**Goal:** A wrapped code cell that makes more than one figure, in a place where figures keep their normal layout, prints one warning for the cell.

**Outcome:** In `float_target` (`wrapped.lua`), a cell with `several` set now takes the context branch. All its figures keep their normal layout, and the first figure prints `the code cell #<label> <context>, so it does not wrap.`, or `makes more than one figure` with no context. A cell in no context with no paragraph after it stays silent, and a table in a cell keeps its own warning. Two-plot cells were added to margin-meta, page-wide-meta, column-meta, and contexts (callout, margin, and a margin cell before a heading). Their snapshots only add lines. README "Where a figure keeps its normal layout", DESIGN.md Goals and the next-block rule, and wrap-mechanisms E4 say so. The margin-meta cell sits above the no-id image, because `typ_summary` gave that image the margin cell's label.

**Decisions:** One cell warning in a context, with the context as its reason, reverses M014's Scope Out clause (per-figure context warnings) and stays within D-010.

**Review:** All 3 criteria verified: an 18-case snapshot script, the README text, verify passing all 97 renders locally and in CI (7m17s). Claim audit: 23 claims read, 1 corrected. Four-lens review, 22 findings: 9 fixed (a no-paragraph margin cell fixture, README and DESIGN wording, the code comment, the M014 reversal record), 2 follow-up to "List margin figures in the summaries" (Typst and LaTeX summaries list no margin figure), 11 rejected (2 edge: a cell that makes a figure and a table float, as at M014). The CI wait stopped once, because the app forbids polling CI from the session. Hygiene: row "Warn once per cell under a context" graduated; M015 row pruned; no lesson captured; four lessons marked used.
